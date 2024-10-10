/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

type Field_Each interface {
	Each() Each
}

type Epoch uint8

const (
	Epoch_Unset Epoch = iota
	Epoch_IssueDate
	Epoch_LastUse
)
