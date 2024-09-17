/* For license and copyright information please see the LEGAL file in the code repository */

package exap

type Status uint8

const (
	EducationAnswer_Unset Status = iota
	EducationAnswer_Passed
	EducationAnswer_Failed
)
