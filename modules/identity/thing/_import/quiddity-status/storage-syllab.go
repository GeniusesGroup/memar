/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity

import (
	"libgo/protocol"
)

type quiddityAsSyllab []byte

func (q *quiddityAsSyllab) QuiddityID() [16]byte       {}
func (q *quiddityAsSyllab) DomainID() uint64           {}
func (q *quiddityAsSyllab) Time() protocol.Time        {}
func (q *quiddityAsSyllab) RequestID() UserRequestUUID {}
