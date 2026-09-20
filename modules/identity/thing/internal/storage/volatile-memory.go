//go:build !ganjine || !mysql

/* For license and copyright information please see the LEGAL file in the code repository */

package storage

import (
	"sync"

	"libgo/protocol"

	qdp "org/modules/quiddity-domain/protocol"
)

var Storage vm
var _ qdp.StorageServices = &Storage

// code generated in memory storage to test the software by any way like unit test or human test.
type vm struct {
	mutex            sync.Mutex
	index_QuiddityID map[[16]byte]qdp.QuiddityDomain
}

func (s *vm) Save(q qdp.QuiddityDomain) (err protocol.Error) {
	s.mutex.Lock()
	var quiddityID = q.QuiddityID()
	var _, ok = s.index_QuiddityID[quiddityID]
	if !ok {
		s.index_QuiddityID[quiddityID] = q
	} else {
		// err =
	}
	s.mutex.Unlock()
	return
}

func (s *vm) Get(quiddityID [16]byte) (q qdp.QuiddityDomain, err protocol.Error) {
	q = s.index_QuiddityID[quiddityID]
	return
}
