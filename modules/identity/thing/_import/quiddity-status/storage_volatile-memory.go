//go:build !libgo

/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity

import (
	"sync"

	"libgo/protocol"

	org "../../protocol"
)

// TODO::: code generated in memory storage to test the software by any way like unit test or human test.
var storage vm
var _ org.Quiddity_StorageServices = &storage

type vm struct {
	mutex              sync.Mutex
	records            map[[16]byte][]org.Quiddity
	ids                [][16]byte
	poolByDepartmentID map[[16]byte][][16]byte
}

func (s *vm) Save(r org.Quiddity) (err protocol.Error) {
	s.mutex.Lock()
	var roleID = r.RoleID()
	var record, ok = s.records[roleID]
	if !ok {
		s.records[roleID] = []org.Role{r}
		s.ids = append(s.ids, roleID)
	} else {
		record = append(record, r)
		// TODO::: check if reference need to update
		s.records[roleID] = record
	}
	s.mutex.Unlock()
	return
}

func (s *vm) Count(roleID [16]byte) (numbers uint64, err protocol.Error) {
	numbers = uint64(len(s.records[roleID]))
	return
}
func (s *vm) Get(roleID [16]byte, versionOffset uint64) (r org.Role, err protocol.Error) {
	r = s.records[roleID][versionOffset]
	return
}
func (s *vm) Last(roleID [16]byte) (r org.Role, numbers uint64, err protocol.Error) {
	numbers, err = s.Count(roleID)
	r, err = s.Get(roleID, numbers-1)
	return
}

func (s *vm) GetIDs(offset, limit uint64) (roleIDs [][16]byte, numbers uint64, err protocol.Error) {
	numbers = uint64(len(s.ids))
	roleIDs = s.ids[offset : offset+limit]
	return
}

func (s *vm) FindByDepartmentID(departmentID [16]byte, offset, limit uint64) (roleIDs [][16]byte, numbers uint64, err protocol.Error) {
	var ok bool
	roleIDs, ok = s.poolByDepartmentID[departmentID]
	if !ok {
		// err=
		return
	}

	numbers = uint64(len(roleIDs))
	roleIDs = roleIDs[offset : offset+limit]
	return
}
