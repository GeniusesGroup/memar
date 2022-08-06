//go:build mysql

/* For license and copyright information please see LEGAL file in repository */

package storage

import (
	"database/sql"

	"github.com/GeniusesGroup/libgo/protocol"
	qdp "github.com/GeniusesGroup/organization/modules/quiddity-domain/protocol"
)

// TODO::: code generated in memory storage to test the software by any way like unit test or human test.
var Storage mysql
var _ dp.StorageServices = &storage

type mysql struct {
	db *sql.DB
}

func (s *mysql) Save(r qdp.QuiddityDomain) (err protocol.Error) {
	const query = "INSERT INTO QuiddityDomain VALUES (?, ?, ?, ?)"
	_, err = s.db.Exec(query, r.QuiddityID(), r.DomainID(), r.RequestID(), r.Time())
	return
}

func (s *mysql) Get(quiddityID [16]byte) (q qdp.QuiddityDomain, err protocol.Error) {
	const query = "SELECT * FROM QuiddityDomain WHERE QuiddityID = ?"
	var rows *sql.Rows
	rows, err = s.db.Query(query, quiddityID)
	// TODO:::
	return
}

// 192/