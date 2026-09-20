/* For license and copyright information please see the LEGAL file in the code repository */

package captcha

// Status use to indicate captcha status
type Status uint8

// Captcha Status
const (
	Status_Created Status = iota
	Status_LastAnswerNotValid
	Status_Solved
)
