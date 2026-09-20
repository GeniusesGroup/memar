/* For license and copyright information please see the LEGAL file in the code repository */

package storage

import (
	"libgo/protocol"
	"libgo/time/utc"

	urp "org/modules/user-request/protocol"
)

type Quiddity struct {
	quiddityID [16]byte
	domainID   uint64
	time       utc.Time
	requestID  [16]byte
}

func (q *Quiddity) QuiddityID() [16]byte           { return q.quiddityID }
func (q *Quiddity) DomainID() uint64               { return q.domainID }
func (q *Quiddity) Time() protocol.Time            { return &q.time }
func (q *Quiddity) RequestID() urp.UserRequestUUID { return q.requestID }

//libgo:impl protocol.Syllab
func (q *Quiddity) FromSyllab(payload []byte, stackIndex uint32) {
	// TODO::: auto generate
}
func (q *Quiddity) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	// TODO::: auto generate
	return
}
func (q *Quiddity) LenOfSyllabStack() uint32 {
	// TODO::: auto generate
	return 0
}
func (q *Quiddity) LenOfSyllabHeap() (ln uint32) {
	// TODO::: auto generate
	return
}
func (q *Quiddity) LenAsSyllab() uint64 {
	return uint64(q.LenOfSyllabStack() + q.LenOfSyllabHeap())
}

//libgo:impl protocol.JSON
func (q *Quiddity) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	// TODO::: auto generate
	return
}
func (q *Quiddity) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	// TODO::: auto generate
	return
}
func (q *Quiddity) LenAsJSON() (ln int) {
	// TODO::: auto generate
	return
}
