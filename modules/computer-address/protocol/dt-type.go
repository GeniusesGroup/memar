/* For license and copyright information please see the LEGAL file in the code repository */

package cap

type Type uint8

const (
	Type_Unset Type = iota
	Type_DomainName // TODO::: WHY? NS system??
	Type_HostName
	Type_IPv4
	Type_IPv6
	Type_GP
)
