/* For license and copyright information please see the LEGAL file in the code repository */

package form_p

type Field_Type interface {
	Type() Type
}

type Type uint64

const (
	Type_Unset     Type = 0
	Type_Anonymous Type = (1 << iota)
	Type_Duration
	Type_StartPoint
	Type_AllowToEdit
	Type_MaxAttempt

	// No one can made direct answer to this form.
	Type_Criterion
	//
	Type_Quiz
	//
	Type_Survey
	//
	Type_Questionnaire
	//
	Type_Poll

	// TODO::: GUI template for forms?
)
