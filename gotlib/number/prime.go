package number

import (
	"math"
)

type Primes []int

// Returns a list of prime numbers up to (but not including `x`)
// Uses an optimize Sieve of Eratosthenes
func MakePrimes(x int) Primes {
	if x < 2 {
		return []int{}
	}

	a := make([]int, x/2)
	q := int(math.Sqrt(float64(x)) + 1)
	factor := 3

	for factor < q {
		for i := factor; i < x; i += 2 {
			if a[i>>1] == 0 {
				factor = i
				break
			}
		}

		for i := factor * factor; i < x; i += factor * 2 {
			a[i>>1] = 1
		}

		factor += 2
	}

	a[0] = 2
	prime_idx := 1
	for i := 3; i < x; i += 2 {
		if a[i>>1] == 0 {
			a[prime_idx] = i
			prime_idx += 1
		}
	}

	return a[0:prime_idx]
}

// Returns the list of prime factors
func (primes Primes) GetPrimeFactors(x int) []int {
	factors := []int{}
	for _, prime := range primes {
		if x%prime == 0 {
			factors = append(factors, prime)
			x /= prime
		}
		for x%prime == 0 {
			x /= prime
		}
	}
	return factors
}
