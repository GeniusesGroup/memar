/* For license and copyright information please see the LEGAL file in the code repository */

package pa

import (
	"libgo/protocol"
)

// ReqSetOTP :
type ReqSetOTP struct {
	Password         [32]byte `valid:"Password"`
	OTP              uint32
	OTPAdditional    int32
	SecurityQuestion uint16
	SecurityAnswer   string
}

// ResSetOTP :
type ResSetOTP struct {
	OTPPattern   [32]byte
	RecoveryCode [128]byte
}

// SetOTP can be used to enable or renew otp.
func SetOTP(st *protocol.Stream, req *ReqSetOTP) (*ResSetOTP, error) {
	// It always renew OTPPattern && RecoveryCode too

	return nil, nil
}
