/* For license and copyright information please see the LEGAL file in the code repository */

package ggbuService

type Request struct {
	UserID        [16]byte
	UserPublicKey [32]byte `valid:"PublicKey"`
	ThingID       [16]byte
	CipherSuite   uint16 // 0 for not use crypt for headers! not suggest specially in public networks!
}

func (req *Request) validate() error {
	return nil
}

func (req *Request) sRPCDecoder(buf []byte) error {
	return nil
}
