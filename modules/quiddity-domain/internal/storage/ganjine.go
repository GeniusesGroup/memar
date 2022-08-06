//go:build ganjine

/* For license and copyright information please see LEGAL file in repository */

package storage

import (
	"github.com/GeniusesGroup/libgo/protocol"
	qdp "github.com/GeniusesGroup/organization/modules/quiddity-domain/protocol"
)

var storage ganjine
var _ qdp.StorageServices = &storage

// code generated in memory storage to test the software by any way like unit test or human test.
type ganjine struct{}

// Save method set some data and write entire Quiddity record with all indexes.
func (s *ganjine) Save(q qdp.Quiddity) (err protocol.Error) {
	// TODO::: auto generate
	return
}

func (s *ganjine) Get(quiddityID [16]byte) (q qdp.Quiddity, err protocol.Error) {
	// TODO::: auto generate
	return
}
