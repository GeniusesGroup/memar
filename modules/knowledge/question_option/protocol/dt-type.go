/* For license and copyright information please see the LEGAL file in the code repository */

package qo_p

type Type uint16

const (
	Type_Unset   Type = 0
	Type_Correct Type = (1 << iota)

	Type_Limit // QuestionOptionMultipleChoice

	// Without need to be an option to prevent impact on overall result
	Type_Neutral

	Type_ForceToFill_Question
	Type_ForceToFill_Form
	Type_ForceToContinue_Question
	Type_ForceToContinue_Form

	// It will effect on other option analytical.
	Type_Criterion
)
