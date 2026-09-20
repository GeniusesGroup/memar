/* For license and copyright information please see the LEGAL file in the code repository */

package distribution_p

import (
	transaction_p "org/modules/economics/transaction/protocol"
)

type Field_DistributionID interface {
	DistributionID() UUID
}

type UUID transaction_p.UUID
