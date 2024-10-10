/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

type Field_Epoch interface {
	Epoch() Epoch
}

// Each time use
type Each uint8

func (dt *Each) Optional() bool { return false }
