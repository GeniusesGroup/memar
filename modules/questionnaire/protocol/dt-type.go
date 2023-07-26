/* For license and copyright information please see the LEGAL file in the code repository */

package qp

type Type uint16

const (
	Type_Unset Type = 0
	Type_Quiz  Type = (1 << iota)
	Type_Anonymous
	Type_Duration
	Type_StartPoint
	Type_AllowToEdit
	Type_Form
	Type_MaxAttempt

	// No one can made direct answer to this questionnaire.
	Type_Criterion

	// TODO::: Template for forms?
)
