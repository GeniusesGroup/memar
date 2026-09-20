/* For license and copyright information please see the LEGAL file in the code repository */

package fai

import (
	account_p "org/modules/economics/account/protocol"
)

type (
	BS_Register_Request interface {
		account_p.Field_AccountID
		ID() ID
	}
)

type (
	BS_Get_Request interface {
		account_p.Field_AccountID
	}
	BS_Get_Response = DataModel
)
