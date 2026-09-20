/* For license and copyright information please see the LEGAL file in the code repository */

package graph_p

import (
	container_p "memar/computer/adt/container/protocol"

	account_p "org/modules/economics/account/protocol"
	// card_p "org/modules/vertices/card/protocol"
	thing_p "org/modules/identity/thing/protocol"
	user_p "org/modules/identity/user/protocol"
)

type (
	BS_Register_Request interface {
		account_p.Field_AccountID
		// card_p.Field_CardID
		Priority() uint64
		// Field_Status
	}
)

type (
	BS_Get_Request interface {
		account_p.Field_AccountID
		// card_p.Field_CardID
	}
	BS_Get_Response = DataModel
)

type (
	BS_GetIDs_Request interface {
		container_p.Pagination_Offset_Request
	}
	BS_GetIDs_Response interface {
		// estate_p.Field_EstateIDs
		container_p.Pagination_Response
	}
)

type (
	BS_FindByUserID_Request interface {
		user_p.Field_UserUUID
		container_p.Pagination_Offset_Request
	}
	BS_FindByUserID_Response interface {
		thing_p.Field_ThingsUUID
		container_p.Pagination_Response
	}
)

// LIST_ProductIDs_BY_OrgID_AND_LabelID(orgID org_p.UUID, t Type, offset, limit uint64) (productIDs []pp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// LIST_ProductIDs_BY_OrgID(orgID org_p.UUID, offset, limit uint64) (productIDs []pp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// LIST_OrgIDs_By_ProductID(productID pp.UUID, offset, limit uint64) (orgIDs []org_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

// FindBySubstitute(substituteID thing_p.UUID, offset, limit uint64) (quiddityIDs []thing_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// ListQuiddities(complementID thing_p.UUID, offset, limit uint64) (quiddityIDs []thing_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
