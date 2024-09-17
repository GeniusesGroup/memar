/* For license and copyright information please see the LEGAL file in the code repository */

package vdp

type Epoch uint8

const (
	Epoch_Unset Epoch = iota
	Epoch_IssueDate
	Epoch_LastUse
)
