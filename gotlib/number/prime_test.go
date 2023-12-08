package number

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMakePrimes(t *testing.T) {
	primes := MakePrimes(10)
	assert.Equal(t, Primes{2, 3, 5, 7}, primes)

	primes = MakePrimes(20)
	assert.Equal(t, Primes{2, 3, 5, 7, 11, 13, 17, 19}, primes)

}

func TestGetPrimeFactors(t *testing.T) {
	primes := MakePrimes(100)

	assert.Equal(t, []int{2, 5}, primes.GetPrimeFactors(10))
	assert.Equal(t, []int{2, 11}, primes.GetPrimeFactors(88))
	assert.Equal(t, []int{7, 11}, primes.GetPrimeFactors(77))
	assert.Equal(t, []int{61}, primes.GetPrimeFactors(61))
}
