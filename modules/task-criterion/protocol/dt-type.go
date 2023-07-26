/* For license and copyright information please see the LEGAL file in the code repository */

package tcp

type Type uint8

const (
	Type_Unset Type = iota
	Type_Progress
	Type_Probability_Win
	Type_Probability_Failure
	Type_StoryPoint // Agile/Scrum
	Type_Risk       // TODO::: risk rate is calculated data or ... ?
)
