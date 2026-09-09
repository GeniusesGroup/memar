/* For license and copyright information please see the LEGAL file in the code repository */

package label

type Law interface {
	HumanCodes() string
	Goal() string
	Explanation() string
	ExecutiveGuarantee() string
	ComputerCodes() string
}
