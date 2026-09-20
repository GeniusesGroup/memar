/* For license and copyright information please see the LEGAL file in the code repository */

package domain_p

type Field_Name interface {
	DomainName() DomainName
}

// unique name in the computer world
type DomainName string
