/* For license and copyright information please see the LEGAL file in the code repository */

package bp

type Type uint16

// https://www.linkedin.com/pulse/5-budgeting-methods-everyone-should-know-about-advantages-ehab-sobhy/
const (
	Type_Unset Type = iota
	Type_Zero_based
	Type_Incremental
	Type_Activity_Based
	Type_Value_Proposition
	Type_Flexible
)
