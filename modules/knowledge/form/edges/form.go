/* For license and copyright information please see the LEGAL file in the code repository */

package label

// TODO::: product, Marketing, law, invoice, education, department, content, estate,

const (
	Type_Anonymous = (1 << iota)
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
