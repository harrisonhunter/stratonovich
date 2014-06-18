package hmm

import (
	// "fmt"
	"errors"
	"io/ioutil"
	"math"
	"math/rand"
	"strconv"
	"strings"
)

func Normal_Sample(mean float64, std float64) float64 {
	return rand.NormFloat64()*std + mean
}

func Normal_PDF(μ float64, σ float64) func(x float64) float64 {
	normal_normalizer := 0.3989422804014327 / σ
	return func(x float64) float64 { return normal_normalizer * math.Exp(-1*(x-μ)*(x-μ)/(2*σ*σ)) }
}

func NextExp(λ float64) float64 { return rand.ExpFloat64() / λ }

func Exp(λ float64) func() float64 { return func() float64 { return NextExp(λ) } }

// Probability density function
func Gamma_PDF(k float64, θ float64) func(x float64) float64 {
	return func(x float64) float64 {
		if x < 0 {
			return 0
		}
		return math.Pow(x, k-1) * math.Exp(-x/θ) / (math.Gamma(k) * math.Pow(θ, k))
	}
}

// Value of the probability density function at x
func Gamma_PDF_At(k, θ, x float64) float64 {
	pdf := Gamma_PDF(k, θ)
	return pdf(x)
}

// Random value drawn from the distribution
func Gamma_Sample(α float64, λ float64) float64 {
	if α == float64(int(α)) && α <= 15 {
		x := NextExp(λ)
		for i := 1; i < int(α); i++ {
			x += NextExp(λ)
		}
		return x
	}

	// if α < 0.75 {
	// return RejectionSample(Gamma_PDF(α, λ), Exp_PDF(λ), Exp(λ), 1)
	// }
	a := α - 1
	b := 0.5 + 0.5*math.Sqrt(4*α-3)
	c := a * (1 + b) / b
	d := (b - 1) / (a * b)
	s := a / b
	p := 1.0 / (2 - math.Exp(-s))
	var x, y float64
	for i := 1; ; i++ {
		u := rand.Float64()
		if u > p {
			var e float64
			for e = -math.Log((1 - u) / (1 - p)); e > s; e = e - a/b {
			}
			x = a - b*e
			y = a - x
		} else {
			x = a - b*math.Log(u/p)
			y = x - a
		}
		u2 := rand.Float64()
		if math.Log(u2) <= a*math.Log(d*x)-x+y/b+c {
			break
		}
	}
	return x / λ
}

// func My_Dirichlet_Sample(params []float64) []float64 {
// 	var gamma = [len(params)]float64{}
// 	var sample = [len(params)]float64{}
// 	sum := 0.0
// 	for i := 0; i < len(params); i++ {
// 		gamma[i] = Gamma_Sample(params[i], 1)
// 		sum += gamma[i]
// 	}
// 	for j := 0; i < len(params); j++ {
// 		sample[i] = gamma[i] / sum
// 	}
// 	return sample
// }

func Dirichlet_Sample(α []float64) []float64 {
	x := make([]float64, len(α))
	sum := 0.0
	for i := 0; i < len(α); i++ {
		x[i] = Gamma_Sample(α[i], 1.0)
		sum += x[i]
	}
	for i := 0; i < len(α); i++ {
		x[i] /= sum
	}
	return x
}

// func Dirichlet(α []float64) func() []float64 {
// return func() []float64 { return NextDirichlet(α) }
// }

type Parameters struct {
	config                                   Configuration
	d, n                                     int
	ones, x                                  []int
	y                                        []float64
	epsilon, minYk, maxYk, r, k, alpha, g, h float64
	priors, means, trans                     []float64
	beta, sigma                              float64
}

func (p Parameters) Init(config Configuration, ys []float64, n int) {
	p.config = config
	p.d = int(config.h_states)
	p.y = ys
	min := math.Inf(-1)
	max := math.Inf(1)
	for i := 0; i < len(ys); i++ {
		if ys[i] < min {
			min = ys[i]
		}
		if ys[i] > max {
			max = ys[i]
		}
	}
	p.n = n
	p.minYk = min
	p.maxYk = max
	p.epsilon = (min + max) / 2.0
	p.r = max - min
	p.k = (1.0 / p.r) * (1.0 / p.r)
	p.alpha = 2.0
	p.g = 0.2
	p.h = (10.0 / p.r) * (10.0 / p.r)
	ones := make([]float64, p.d)
	for i := 0; i < p.d; i++ {
		ones[i] = 1
	}
	p.priors = Dirichlet_Sample(ones)
	p.beta = Gamma_Sample(p.g, p.h)
	p.sigma = math.Sqrt(1.0 / Gamma_Sample(p.alpha, p.beta))
	means := make([]float64, p.d)
	trans := make([][]float64, p.d)
	for i := 0; i < p.d; i++ {
		means[i] = Normal_Sample(p.epsilon, 1.0/p.k)
		trans[i] = Dirichlet_Sample(ones)
	}
	for i := 0; i < p.d; i++ {
		ones[i] = ones[i] / float64(p.d)
	}
	x := make([]int, p.d)
	for i := 0; i < p.d; i++ {
		x[i], _ = select_random(ones)
	}
	p.x = x
}

func select_random(choices []float64) (int, error) {
	upto := 0.0
	for i := 0; i < len(choices); i++ {
		if upto+choices[i] >= rand.Float64() {
			return i, nil
		}
		upto += choices[i]
	}
	if upto > 0 {
		return len(choices), nil
	}
	return 0, errors.New("should not get here")
}

func get_I(params Parameters, i int) int {
	if params.x[0] == i {
		return 1
	} else {
		return 0
	}
}

func get_n(params Parameters, i int) int {
	sum := 0
	for k := 0; k < params.n; k++ {
		if params.x[k] == i {
			sum += 1
		}
	}
	return sum
}

func get_n_trans(params Parameters, i int, j int) int {
	sum := 0
	for k := 1; k < params.n; k++ {
		if params.x[k] == j && params.x[k-1] == i {
			sum += 1
		}
	}
	return sum
}

func get_s(params Parameters, i int) float64 {
	sum := 0.0
	for k := 0; k < params.n; k++ {
		if params.x[k] == i {
			sum += params.y[k]
		}
	}
	return sum
}

func eq_1(params Parameters) []float64 {
	Is := make([]float64, params.d)
	for i := 0; i < params.d; i++ {
		Is[i] = float64(get_I(params, i) + 1)
	}
	return Dirichlet_Sample(Is)
}

func eq_2(params Parameters, i int) []float64 {
	ns := make([]float64, params.d)
	for j := 0; j < params.d; j++ {
		ns[j] = float64(get_n_trans(params, i, j) + 1)
	}
	return Dirichlet_Sample(ns)
}

func eq_3(params Parameters, i int) float64 {
	mean := (get_s(params, i) + params.k*params.epsilon*params.sigma*params.sigma) / (float64(get_n(params, i)) + params.k + params.sigma*params.sigma)
	std := (params.sigma * params.sigma) / (float64(get_n(params, i)) + params.k + params.sigma*params.sigma)
	return Normal_Sample(mean, std)
}

func eq_4(params Parameters) float64 {
	shape := params.alpha + float64(params.n)/2.0
	a := 0.0
	for k := 1; k < params.n; k++ {
		a += (params.y[k] - params.means[params.x[k]]) * (params.y[k] - params.means[params.x[k]])
	}
	scale := params.beta + a/2.0
	return math.Sqrt(1.0 / Gamma_Sample(shape, 1.0/scale))
}

func eq_5(params Parameters) float64 {
	shape := params.g + params.alpha
	scale := params.h + 1.0/(params.sigma*params.sigma)
	return Gamma_Sample(shape, 1.0/scale)
}

func eq_6(params Parameters) []int {
	probs := forward_backward(params)
	seq := make([]int, len(probs))
	for i := 0; i < len(probs); i++ {
		seq[i], _ = select_random(probs[i])
	}
	return seq
}

func readLines(path string) []string {
	content, err := ioutil.ReadFile(path)
	if err != nil {
		//Do something
	}
	lines := strings.Split(string(content), "\n")
	return lines
}

type Configuration struct {
	comment, data_path, method, prior string
	h_states, o_vars, o_states        int64
	// o_vars                            int
	// which_vars []float64
}

func parse_config(path_to_config string) Configuration {
	// config_fields := [...]string{"comment", "data_path", "h_states", "o_vars", "which_vars", "method", "prior", "o_states"}
	c := Configuration{}
	lines := readLines(path_to_config)
	content := make([]string, len(lines))
	for i := 0; i < len(lines); i++ {
		lines[i] = strings.TrimSpace(lines[i])
		content[i] = strings.Split(lines[i], " ")[1]
	}
	// for i := 0; i < len(content); i++ {
	// 	if i == 2 || i == 3 || i == 7 {
	// 		content[i], _ = strconv.ParseInt(content[i], 10, 0)
	// 	}
	// }
	c.comment = content[0]
	c.data_path = content[1]
	c.h_states, _ = strconv.ParseInt(content[2], 10, 0)
	// c.o_vars, _ = strconv.ParseInt(content[3], 10, 0)
	// c.which_vars = content[4]
	c.method = content[5]
	c.prior = content[6]
	c.o_states, _ = strconv.ParseInt(content[7], 10, 0)
	return c
}

func load_data(config Configuration) []float64 {
	lines := readLines(config.data_path)
	content := make([]float64, len(lines))
	for i := 0; i < len(lines); i++ {
		lines[i] = strings.TrimRight(lines[i], "\n")
		content[i], _ = strconv.ParseFloat(lines[i], 64)
	}
	return content
}

func create_params_object(config Configuration) Parameters {
	ys := load_data(config)
	n := len(ys)
	p := Parameters{}
	p.Init(config, ys, n)
	return p
}
