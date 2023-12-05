import Foundation

func getIntArray(_ fname: String) -> [Int] {
    do {
        let lines = try String(contentsOfFile: fname).split(separator: "\n")
        return lines.map({ Int($0, radix: 2) ?? 0 })
    } catch {
        print(error.localizedDescription)
    }
    return []
}

func calcRating(arr: [Int], msb: Int, op: (Int, Int) -> Bool) -> Int {
    var i = msb
    var _arr = arr
    while i > 0 {
        i -= 1
        let n1 = _arr.reduce(0, { $1>>i & 1 == 1 ? $0 + 1 : $0 })
        let n0 = _arr.count - n1
        let want = op(n1, n0) ? 1 : 0
        _arr = _arr.filter{ $0>>i & 1 == want }
        /*print("i", i, "n0", n0, "n1", n1, "want", want, "_arr:", _arr)*/
        if _arr.count <= 1 { break }
    }
    return _arr[0]
}

func part2() {
    let arr = getIntArray("day03.txt")
    var msb = 0
    for var v in arr {
        var i = 0
        while v > 0 {
            v >>= 1
            i += 1
        }
        msb = max(msb, i)
    }

    let oxy = calcRating(arr: arr, msb: msb, op: >=)
    let co2 = calcRating(arr: arr, msb: msb, op: <)
    print(oxy * co2)
}

func part1() {
    let arr = getIntArray("day03.txt")
    var freq = Array(repeating: 0, count: 16)
    for var v in arr {
        var i = 0
        while v > 0 {
            freq[i] += v & 1
            v >>= 1
            i += 1
        }
    }

    var gamma = 0, epsilon = 0, i = freq.firstIndex(of: 0) ?? 0
    let half = arr.count / 2
    while i > 0 {
        i -= 1
        if freq[i] >= half {
            gamma |= 1
        } else {
            epsilon |= 1
        }
        gamma <<= 1
        epsilon <<= 1
    }
    gamma >>= 1
    epsilon >>= 1
    print(gamma * epsilon)
}

part1()
part2()
