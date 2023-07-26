/* For license and copyright information please see the LEGAL file in the code repository */

package brup

type Type uint8

const (
	Type_Unset Type = iota
	Type_Suggester
	Type_Rectifier
	Type_Executor
	Type_Quality_Controller
)
