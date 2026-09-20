/* For license and copyright information please see the LEGAL file in the code repository */

package otp

import (
	"crypto/sha512"
	"encoding/binary"
	"testing"

	"memar/time/earth"
	"memar/time/unix"
)

var otpSecurityKey = []byte{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8}

func TestGenerateTimeOTP(t *testing.T) {
	var otpReq = GenerateTimeOTPReq{
		Hasher:     sha512.New512_256(),
		SecretKey:  otpSecurityKey,
		Additional: make([]byte, 8),
		Period:     earth.SecondInDay,
		Digits:     6,
	}
	binary.LittleEndian.PutUint64(otpReq.Additional, 9171170268)
	// otpReq.SecretKey = strconv.AppendUint(otpSecurityKey, 9171170267, 10)
	var timeOTP, err = GenerateTimeOTP(&otpReq)
	if err != nil {
		t.Error(err)
	}
	t.Error("OTP time:", unix.Now().ElapsedBySecond(otpReq.Period))
	t.Error("OTP:", timeOTP)
}

/*
   totp_test.go:29: OTP time: 18546
    totp_test.go:30: OTP: 326987

	totp_test.go:29: OTP time: 18546
    totp_test.go:30: OTP: 252387
*/
