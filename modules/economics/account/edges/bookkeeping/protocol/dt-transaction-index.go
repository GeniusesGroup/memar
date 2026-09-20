/* For license and copyright information please see the LEGAL file in the code repository */

package bookkeeping_p

import (
	container_p "memar/computer/adt/container/protocol"
)

type Field_TransactionIndex interface {
	TransactionIndex() TransactionIndex
}

// TransactionIndex will auto increment number in each AccountID
type TransactionIndex container_p.ElementIndex
