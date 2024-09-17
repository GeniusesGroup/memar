/* For license and copyright information please see the LEGAL file in the code repository */

package br_p

type Field_LogicType interface {
	LogicType() LogicType
}

type LogicType uint64

const (
	LogicType_Unset LogicType = iota
	LogicType_Statement
	LogicType_WASM
	LogicType_DSL // TODO::: can indicate in very general type or need to indicate the supported languages?

	// TODO::: Add other portable binaries.
	// LogicType_
)
