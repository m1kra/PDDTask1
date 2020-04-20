import subprocess
import time

from pyspark.sql.functions import udf, col
from pyspark.ml.feature import NGram, CountVectorizer, Normalizer
from pyspark.ml.linalg import VectorUDT, Vectors
from pyspark.ml.clustering import KMeans, BisectingKMeans
from pyspark.ml.evaluation import ClusteringEvaluator


class SummaryBuilder:
    def __init__(self):
        self._rep = []

    def add(self, msg):
        self._rep.append(str(msg))
        print(msg)

    def p(self, msg):
        self._rep.append(str(msg))
        print(msg)

    def h1(self, msg):
        self._rep.append('\n\n##' + str(msg))
        print('\n\n')
        print(msg)

    def h2(self, msg):
        self._rep.append('\n###' + str(msg))
        print('\n')
        print(msg)

    def h3(self, msg):
        self._rep.append('\n####' + str(msg))
        print('\n')
        print(msg)

    def log(self, msg):
        self._rep.append(str(msg))
        print(msg)

    def build(self):
        res = '\n'.join(self._rep)
        hadoop_path = '/opt/hadoop-2.9.2/bin/hadoop'
        subprocess.check_call(
            f"echo '{res}' | {hadoop_path} fs -put -f - report.md",
            shell=True
        )


sb = SummaryBuilder()


def load_data(spark):
    return (
        spark.read.format("csv")
        .option("sep", "\t")
        .option("inferSchema", "true")
        .option("header", "true")
        .load("hdfs://master:9000/user/vagrant/data.csv")
        .rdd
        .map(lambda r: (r[0], list(r[1])))
        .toDF(['id', 'sequence'])
        # .select(to_list(col("Sequence")).alias("sequence"))
        # for some reason this^ doesn't work sometimes
        # where to_list = udf(list, ArrayType(FloatType()))
    )


def calculate_vectors(data, n=2, binary=False):
    ngram = NGram(n=n, inputCol="sequence", outputCol="ngrams")
    ngramDataFrame = ngram.transform(data)
    ngrams = ngramDataFrame.select("ngrams")
    cvectorizer = CountVectorizer(
        inputCol="ngrams", outputCol="vec", binary=binary
    )
    model = cvectorizer.fit(ngrams)
    return model.transform(ngrams).select("vec")


def calculate_for_comparison(vectors):
    def basic_stats(vector):
        return (
            float(len(vector)),
            float(vector.numNonzeros()),
            float(vector.norm(1)),
            float(vector.norm(2))

        )
    stats = (
        vectors
        .rdd
        .map(lambda r: basic_stats(r[0]))
        .toDF()
    )
    res = []
    for colname in stats.schema.names:
        res.append(max(stats.select(colname).collect())[0])
    return res


def compare_sparse_dense(data):
    sb.h1("Dense vs sparse vectors comparison")
    sb.p(
        "Done by calculating some basic statistics, like\n"
        "\t-vector length,"
        "\t-number of nonzero entries,"
        "\t-l1 norm,"
        "\t-l2 norm."
        "The data here is limited to only first 100 records."
        "For larger number of records, computations with dense "
        "vector would take too much time and memory."
    )
    ns = (3, 5)
    limited_data = data.limit(100)

    def to_dense(sv):
        return Vectors.dense(sv.toArray())
    to_dense = udf(to_dense, VectorUDT())

    for n in ns:
        sb.h2(
            f"Shingle length: {n}"
        )
        sv = calculate_vectors(limited_data, n, binary=False).cache()
        start = time.time()
        # this method of measauring time isn't the best
        # but at least it is fair;
        # mind collect in `calculate_for_comparison`
        calculate_for_comparison(sv)
        sparse = time.time() - start
        dv = sv.select(to_dense(col("vec")))
        start = time.time()
        stats = calculate_for_comparison(dv)
        dense = time.time() - start
        sb.p(
            f"computation time using: "
            f"sparse vectors - {sparse:.2f}s, dense vectors - {dense:.2f}s.\n"
            f"\tvector length: {stats[0]}\n"
            f"\tmax number of nonzero entries: {stats[1]}\n"
            f"\tmax l1 norm: {stats[2]}\n"
            f"\tmax Euclidian norm: {stats[3]}."
        )
    sb.p(
        "One can see that, "
        "for short or long n-grams, vectors are quite sparse.\n"
        "Clearly, dense vectors here are not only slower, but "
        "they consume a lot more memory.\n"
    )


def normalize_vectors(vectors):
    normalizer = Normalizer(inputCol="features", outputCol="nfeatures", p=2)
    return normalizer\
        .transform(vectors)\
        .select("nfeatures")\
        .withColumnRenamed("nfeatures", "features")


def cluster(data):
    sb.h1("Compariosn of clustering algorithms and parameters")
    euclidian_evaluator = ClusteringEvaluator()
    cosine_evaluator = ClusteringEvaluator()\
        .setDistanceMeasure("cosine")

    sb.h2("Using k-means|| algorithm")
    sb.h3("Not normalized vectors - squared Euclidian distance")
    for binary in (True, False):
        for n in (3, 4, 5):
            vectors = calculate_vectors(data, n=n, binary=binary)\
                .withColumnRenamed("vec", "features")
            sb.p(
                f'Parameters: n (in n-grams): {n}; vector-type (0/1 or counts)'
                f': {"binary" if binary else "counts"}.'
            )
            for k in (7, 8, 9):
                kmeans = KMeans().setK(k).setSeed(1)
                model = kmeans.fit(vectors)
                predictions = model.transform(vectors)
                sb.p(f'\nk-means algorithm with k={k}')
                silhouette = euclidian_evaluator.evaluate(predictions)
                sb.p(f'silhouette with euclidian distance: {silhouette}')
                silhouette = cosine_evaluator.evaluate(predictions)
                sb.p(f'silhouette with cosine similarity: {silhouette}')
                wsse = model.computeCost(vectors)
                sb.p(f'wsse: {wsse}')

    sb.p(
        '\nFor example k=8 seems reasonable, '
        'because of slight spike is silhouette.'
    )

    n, binary = 5, False
    sb.h3("Normalized vectors - cosine similarity")
    vectors = normalize_vectors(vectors)
    sb.p(
        f'Parameters: n (in n-grams): {n}; vector-type (0/1 or counts)'
        f': {"binary" if binary else "counts"}.'
    )
    for k in (7, 8, 9):
        kmeans = KMeans().setK(k).setSeed(1)
        model = kmeans.fit(vectors)
        predictions = model.transform(vectors)
        sb.p(f'\nk-means algorithm with k={k}')
        silhouette = euclidian_evaluator.evaluate(predictions)
        sb.p(f'silhouette with euclidian distance: {silhouette}')
        silhouette = cosine_evaluator.evaluate(predictions)
        sb.p(f'silhouette with cosine similarity: {silhouette}')
        wsse = model.computeCost(vectors)
        sb.p(f'wsse: {wsse}')

    sb.p(
        '\nHowever k=8 is not so good, '
        'for normalized data.'
    )

    sb.h2("Using BisectingKMeans algorithm")
    sb.p(
        f'Parameters: n (in n-grams): {n}; vector-type (0/1 or counts)'
        f': {"binary" if binary else "counts"}.\n Normalized vectors.'
    )
    for k in (7, 8, 9):
        kmeans = BisectingKMeans().setK(k).setSeed(1)
        model = kmeans.fit(vectors)
        predictions = model.transform(vectors)
        sb.p(f'\nk-means algorithm with k={k}')
        silhouette = euclidian_evaluator.evaluate(predictions)
        sb.p(f'silhouette with euclidian distance: {silhouette}')
        silhouette = cosine_evaluator.evaluate(predictions)
        sb.p(f'silhouette with cosine similarity: {silhouette}')
        wsse = model.computeCost(vectors)
        sb.p(f'wsse: {wsse}')


def main(spark, sc):
    data = load_data(spark)
    compare_sparse_dense(data)
    cluster(data)
