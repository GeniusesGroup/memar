//go:build mysql

/* For license and copyright information please see the LEGAL file in the code repository */

package role

import (
	org "../../protocol"
	"libgo/protocol"
)

var storage mysql
var _ org.Role_StorageServices = &storage

type mysql struct{}

func (s *mysql) Save(r org.Role) (err protocol.Error) {
	return
}

func (s *mysql) Count(roleID [16]byte) (numbers uint64, err protocol.Error) {
	return
}
func (s *mysql) Get(roleID [16]byte, versionOffset uint64) (r org.Role, err protocol.Error) {
	return
}
func (s *mysql) Last(roleID [16]byte) (r org.Role, numbers uint64, err protocol.Error) {
	return
}

func (s *mysql) GetIDs(offset, limit uint64) (roleIDs [][16]byte, numbers uint64, err protocol.Error) {
	return
}

func (s *mysql) FindByDepartmentID(departmentID [16]byte, offset, limit uint64) (roleIDs [][16]byte, numbers uint64, err protocol.Error) {
	return
}
