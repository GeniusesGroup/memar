/* For license and copyright information please see LEGAL file in repository */

package storage

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/utc"
)

type Quiddity struct {
	quiddityID [16]byte
	domainID   uint64
	time       utc.Time
	requestID  [16]byte
}

func (q *Quiddity) QuiddityID() [16]byte { return q.quiddityID }
func (q *Quiddity) DomainID() uint64     { return q.domainID }
func (q *Quiddity) Time() protocol.Time  { return &q.time }
func (q *Quiddity) RequestID() [16]byte  { return q.requestID }

// Syllab codec
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

// JSON codec
func (q *Quiddity) FromJSON(payload []byte) (err protocol.Error) {
	// TODO::: auto generate
	return
}
func (q *Quiddity) ToJSON(payload []byte) []byte {
	// TODO::: auto generate
	return nil
}
func (q *Quiddity) LenAsJSON() (ln int) {
	// TODO::: auto generate
	return
}
