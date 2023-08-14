/* For license and copyright information please see the LEGAL file in the code repository */

package pdp

type Epoch uint8

const (
	Epoch_Unset Epoch = iota
	Epoch_FirstUse
	Epoch_PurchaseTime
)
