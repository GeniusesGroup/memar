/* For license and copyright information please see the LEGAL file in the code repository */

package qop

type AlgorithmType uint8

const (
	AlgorithmType_Unset AlgorithmType = iota
	AlgorithmType_UserID
	AlgorithmType_StaffID
	AlgorithmType_RegisteredTime
)
