

##Dense vs sparse vectors comparison
Done by calculating some basic statistics, like
	-vector length,	-number of nonzero entries,	-l1 norm,	-l2 norm.The data here is limited to only first 100 records.For larger number of records, computations with dense vector would take too much time and memory.

###Shingle length: 3
computation time using: sparse vectors - 2.42s, dense vectors - 6.74s.
	vector length: 7331.0
	max number of nonzero entries: 1538.0
	max l1 norm: 2738.0
	max Euclidian norm: 203.94116798724087.

###Shingle length: 5
computation time using: sparse vectors - 1.92s, dense vectors - 35.81s.
	vector length: 47199.0
	max number of nonzero entries: 179.0
	max l1 norm: 385.0
	max Euclidian norm: 80.77747210701756.
One can see that, for short or long n-grams, vectors are quite sparse.
Clearly, dense vectors here are not only slower, but they consume a lot more memory.



##Compariosn of clustering algorithms and parameters

###Using k-means|| algorithm

####Not normalized vectors - squared Euclidian distance
Parameters: n (in n-grams): 3; vector-type (0/1 or counts): binary.

k-means algorithm with k=7
silhouette with euclidian distance: -0.010987134823122345
silhouette with cosine similarity: -0.10592837202409335
wsse: 8201986.8456782

k-means algorithm with k=8
silhouette with euclidian distance: 0.06013410227596062
silhouette with cosine similarity: -0.12262764995924909
wsse: 8215872.631331706

k-means algorithm with k=9
silhouette with euclidian distance: 0.041361903529883816
silhouette with cosine similarity: -0.1234201517453706
wsse: 8195206.348647729
Parameters: n (in n-grams): 4; vector-type (0/1 or counts): binary.

k-means algorithm with k=7
silhouette with euclidian distance: -0.4069060878059512
silhouette with cosine similarity: -0.008185419450407655
wsse: 10795194.389304386

k-means algorithm with k=8
silhouette with euclidian distance: -0.16270062957758927
silhouette with cosine similarity: -0.00938531771037638
wsse: 10794118.545177355

k-means algorithm with k=9
silhouette with euclidian distance: -0.29077933255600946
silhouette with cosine similarity: -0.014927886497425968
wsse: 10789949.687974436
Parameters: n (in n-grams): 5; vector-type (0/1 or counts): binary.

k-means algorithm with k=7
silhouette with euclidian distance: -0.22546297376334695
silhouette with cosine similarity: -0.0027466983147014772
wsse: 4535809.140712099

k-means algorithm with k=8
silhouette with euclidian distance: -0.13716266708030725
silhouette with cosine similarity: -0.005227580326948814
wsse: 4534280.44893647

k-means algorithm with k=9
silhouette with euclidian distance: -0.21207869041119423
silhouette with cosine similarity: -0.005272548564030772
wsse: 4532575.01166046
Parameters: n (in n-grams): 3; vector-type (0/1 or counts): counts.

k-means algorithm with k=7
silhouette with euclidian distance: 0.4117563023076396
silhouette with cosine similarity: -0.10831664392527227
wsse: 16655022.73466135

k-means algorithm with k=8
silhouette with euclidian distance: 0.4444503334575805
silhouette with cosine similarity: -0.11149544603645556
wsse: 16436782.121679224

k-means algorithm with k=9
silhouette with euclidian distance: 0.3918970491051802
silhouette with cosine similarity: -0.11090192781378738
wsse: 16164406.912754193
Parameters: n (in n-grams): 4; vector-type (0/1 or counts): counts.

k-means algorithm with k=7
silhouette with euclidian distance: 0.022646983611309596
silhouette with cosine similarity: -0.006748726504511696
wsse: 13958633.665119624

k-means algorithm with k=8
silhouette with euclidian distance: 0.022709657793868104
silhouette with cosine similarity: -0.008035873066467216
wsse: 13957524.377911385

k-means algorithm with k=9
silhouette with euclidian distance: 0.27364358613732226
silhouette with cosine similarity: -0.022043145622717784
wsse: 13760869.079016086
Parameters: n (in n-grams): 5; vector-type (0/1 or counts): counts.

k-means algorithm with k=7
silhouette with euclidian distance: 0.19571327641117017
silhouette with cosine similarity: -0.0014220223494500464
wsse: 6302587.790455174

k-means algorithm with k=8
silhouette with euclidian distance: 0.3133400362977703
silhouette with cosine similarity: -0.0019592712517406147
wsse: 6241732.938493142

k-means algorithm with k=9
silhouette with euclidian distance: -0.2704056026886546
silhouette with cosine similarity: -0.002138579133688861
wsse: 6241229.449716041

For example k=8 seems reasonable, because of slight spike is silhouette.

####Normalized vectors - cosine similarity
Parameters: n (in n-grams): 5; vector-type (0/1 or counts): counts.

k-means algorithm with k=7
silhouette with euclidian distance: 0.004696756224323424
silhouette with cosine similarity: 0.0046482268555681295
wsse: 20159.036844999508

k-means algorithm with k=8
silhouette with euclidian distance: 0.0038055264376165385
silhouette with cosine similarity: 0.0037569272682950257
wsse: 20162.021425862815

k-means algorithm with k=9
silhouette with euclidian distance: 0.0007174886942857259
silhouette with cosine similarity: 0.0006696462269342867
wsse: 20243.992597474702

However k=8 is not so good, for normalized data.

###Using BisectingKMeans algorithm
Parameters: n (in n-grams): 5; vector-type (0/1 or counts): counts.
 Normalized vectors.

k-means algorithm with k=7
silhouette with euclidian distance: 0.0031177967533110164
silhouette with cosine similarity: 0.0030687463048622997
wsse: 20085.595479231077

k-means algorithm with k=8
silhouette with euclidian distance: 0.0015305433490717503
silhouette with cosine similarity: 0.0014814981213629225
wsse: 20076.61790943599

k-means algorithm with k=9
silhouette with euclidian distance: 0.0016526398381013982
silhouette with cosine similarity: 0.001604486018001909
wsse: 20072.838309768355
