//go:build !mysql

/* For license and copyright information please see the LEGAL file in the code repository */

package role

import (
	"sync"

	"libgo/protocol"

	org "../../protocol"
)

var storage vm
var _ org.Role_StorageServices = &storage

type vm struct {
	mutex          sync.Mutex
	ids            [][16]byte
	index_RoleID   map[[16]byte][]org.Role // PrimaryKey
	index_ParentID map[[16]byte][][16]byte
}

func (s *vm) Save(r org.Role) (nv protocol.NumberOfVersion, err protocol.Error) {
	s.mutex.Lock()

	var roleID = r.RoleID()
	var parentID = r.ParentID()
	var records, ok = s.index_RoleID[roleID]
	if !ok {
		s.index_RoleID[roleID] = []org.Role{r}
		s.ids = append(s.ids, roleID)
	} else {
		records = append(records, r)
		s.index_RoleID[roleID] = records
	}
	nv = protocol.NumberOfVersion(len(records))

	var roleIDs [][16]byte
	roleIDs, ok = s.index_ParentID[parentID]
	if !ok {
		s.index_ParentID[parentID] = [][16]byte{roleID}
	} else {
		roleIDs = append(roleIDs, roleID)
		s.index_ParentID[roleID] = roleIDs
	}

	s.mutex.Unlock()
	return
}

func (s *vm) Count(roleID [16]byte) (numbers uint64, err protocol.Error) {
	s.mutex.Lock()
	numbers = uint64(len(s.index_RoleID[roleID]))
	s.mutex.Unlock()
	return
}
func (s *vm) Get(roleID [16]byte, versionOffset uint64) (r org.Role, nv protocol.NumberOfVersion, err protocol.Error) {
	s.mutex.Lock()
	r = s.index_RoleID[roleID][versionOffset]
	s.mutex.Unlock()
	return
}
func (s *vm) FindByParent(parentID [16]byte, offset, limit uint64) (roleIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error) {
	s.mutex.Lock()
	var ok bool
	roleIDs, ok = s.index_ParentID[parentID]
	if !ok {
		// err=
		return
	}

	nv = protocol.NumberOfVersion(len(roleIDs))
	roleIDs = roleIDs[offset : offset+limit]
	s.mutex.Unlock()
	return
}
func (s *vm) GetIDs(offset, limit uint64) (roleIDs [][16]byte, numbers uint64, err protocol.Error) {
	s.mutex.Lock()
	numbers = uint64(len(s.ids))
	roleIDs = s.ids[offset : offset+limit]
	s.mutex.Unlock()
	return
}
