/* For license and copyright information please see the LEGAL file in the code repository */

package trp

type Epoch uint8

const (
	Epoch_Unset     Epoch = 0
	Epoch_IssueDate Epoch = (1 << iota)
	Epoch_LastInterval

	Epoch_Continuously
)
