/* For license and copyright information please see the LEGAL file in the code repository */

package nap

type (
	BS_RegisterNodeAddresses_Req interface{}
	BS_RegisterNodeAddresses_Res interface{}
)

type (
	BS_GetNeighborAddresses_Req interface{}
	BS_GetNeighborAddresses_Res interface {
		Addresses() []Address
	}
)
