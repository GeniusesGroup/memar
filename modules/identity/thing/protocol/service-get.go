/* For license and copyright information please see the LEGAL file in the code repository */

package protocol

type (
	Service_Get_Request interface {
		QuiddityID() [16]byte
	}
	Service_Get_Response = QuiddityDomain
)
