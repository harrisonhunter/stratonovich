with open(path) as f:
    data = f.read().splitlines()
cleaned = [[float(dp[i]) for i in xrange(2, len(dp)) if i % 7 == 2] for dp in [text.split() for text in data]]
with open('test_data.txt', 'w') as f:
    for i in cleaned:
    	for j in i:
        	f.write(str(j) + '\n')
