/* For license and copyright information please see the LEGAL file in the code repository */

package otp

import (
	"encoding/binary"
	"hash"
	"math"

	error_p "memar/process/error/protocol"
	"memar/time/duration"
	"memar/time/unix"
)

// GenerateTimeOTPReq is request structure of GenerateTimeOTP()
type GenerateTimeOTPReq struct {
	Hasher     hash.Hash // e.g. sha512.New512_256()
	SecretKey  []byte
	Additional []byte
	Period     duration.Second
	Digits     uint // number of integers in the OTP. Some apps expect this to be 6 digits, others support more.
}

// GenerateTimeOTP generate and returns
func GenerateTimeOTP(req *GenerateTimeOTPReq) (otp uint64, err error_p.Error) {
	var buf = make([]byte, len(req.SecretKey)+len(req.Additional)+8)
	copy(buf, req.SecretKey)
	copy(buf[len(req.SecretKey):], req.Additional)
	binary.LittleEndian.PutUint64(buf[len(req.SecretKey)+len(req.Additional):], uint64(unix.Now().ElapsedBySecond(req.Period)))

	req.Hasher.Write(buf)
	var hashSum = req.Hasher.Sum(nil)

	// var hm = hmac.New(req.Hasher, req.SecretKey)
	// var time = make([]byte, 8)
	// binary.LittleEndian.PutUint64(time, uint64(unix.Now().ElapsedByDuration(req.Period)))
	// hm.Write(req.Additional)
	// hm.Write(time)
	// var hashSum = hm.Sum(nil)

	var offset = int(hashSum[len(hashSum)-1] & 0xf)
	otp = ((uint64(hashSum[offset]) & 0x7f) << 24) |
		((uint64(hashSum[offset+1] & 0xff)) << 16) |
		((uint64(hashSum[offset+2] & 0xff)) << 8) |
		(uint64(hashSum[offset+3]) & 0xff)

	otp = otp % uint64(math.Pow10(int(req.Digits)))
	return
}

/*
https://tools.ietf.org/html/rfc6238#section-3
https://tools.ietf.org/html/rfc4226#section-5.4

https://github.com/pquerna/otp
https://github.com/xlzd/gotp
https://github.com/diebietse/gotp
https://github.com/hgfischer/go-otp
https://github.com/hexylena/go-otp
*/
