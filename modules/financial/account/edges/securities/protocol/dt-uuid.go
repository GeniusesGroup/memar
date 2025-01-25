/* For license and copyright information please see the LEGAL file in the code repository */

package securities_p

import (
	account_p "org/modules/financial/account/protocol"
)

type Field_SecuritiesAccountID interface {
	SecuritiesAccountID() UUID
}

type UUID account_p.UUID
