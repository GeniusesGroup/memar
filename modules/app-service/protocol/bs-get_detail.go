/* For license and copyright information please see the LEGAL file in the code repository */

package asp

type (
	BS_GetDetail_Request interface {
		OrgID() [32]byte
		Offset() uint64
		Limit() uint64
	}

	BS_GetDetail_Response interface {
		IDs() [][32]byte
	}
)
