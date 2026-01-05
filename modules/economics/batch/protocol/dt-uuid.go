/* For license and copyright information please see the LEGAL file in the code repository */

package batch_p

import (
	account_p "org/modules/financial/account/protocol"
)

type Field_BatchID interface {
	ProductBatchID() UUID
}

type UUID account_p.UUID
