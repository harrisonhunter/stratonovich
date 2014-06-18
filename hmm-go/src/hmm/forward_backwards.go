package hmm

import "math"

func emission_probs(x float64, state int, p Parameters) float64 {
	normal_normalizer := 0.3989422804014327 / p.sigma
	return normal_normalizer * math.Exp(-1*(x-p.means[state])*(x-p.means[state])/(2*p.sigma*p.sigma))
}

func forward_backward(params Parameters) [][]float64 {
	return forward(params)
}

func forward(params Parameters) [][]float64 {
	dists := make([][]float64, len(params.y)+1)
	// var dists = [len(params.y) + 1][params.d]float64{}
	dists[0] = params.priors
	// var dist = [params.d]float64{}
	for j := 0; j < len(params.y); j++ {
		dist := make([]float64, params.d)
		for i := 0; i < params.d; i++ {
			// prev_sum := dists[j][i]
			dist[i] = emission_probs(params.y[j], i, params)
		}
		dists[j+1] = Normalize(dist)
	}
	return dists
}

func Normalize(input []float64) []float64 {
	sum := 0.0
	for i := 0; i < len(input); i++ {
		sum += input[i]
	}
	for i := 0; i < len(input); i++ {
		input[i] /= sum
	}
	return input
}
