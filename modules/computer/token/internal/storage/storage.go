/* For license and copyright information please see the LEGAL file in the code repository */

package pa

import (
	"golang.org/x/crypto/sha3"

	etime "libgo/earth-time"
	"libgo/ganjine"
	"libgo/pehrest"
	"libgo/syllab"
)

const (
	personAuthenticationStructureID uint64 = 16584294238805136187
)

var personAuthenticationStructure = ds.DataStructure{
	URN:             "urn:giti:sabz.city:data-structure:person-authentication",
	ID:              16584294238805136187,
	IssueDate:       1595888151,
	ExpiryDate:      0,
	ExpireInFavorOf: "",
	Status:          protocol.Software_PreAlpha,
	Structure:       PersonAuthentication{},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Person Authentication",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "store real person authenticate data",
	},
	TAGS: []string{
		"",
	},
}

// PersonAuthentication ---Read locale description in personAuthenticationStructure---
type PersonAuthentication struct {
	WriteTime        time.Time `index-hash:"PersonID[hourly]"`
	RequestID        [16]byte // user-request domain
	PersonID         [16]byte `index-hash:"RecordID"` // UUID of Person
	ReferentPersonID [16]byte `index-hash:"PersonID[if,ReferentPersonID]"`
	Status           PersonAuthenticationStatus

	// Person Authentication Factors https://en.wikipedia.org/wiki/Authentication#Factors_and_identity
	PasswordHash  [32]byte
	OTPPattern    [32]byte // https://tools.ietf.org/html/rfc6238
	OTPAdditional int32    // easy to be 2 to 7 digit. https://en.wikipedia.org/wiki/Personal_identification_number
	PublicKey     [32]byte // Hardware key and also use to make OTP for very security sensitive usage
}

// SaveNew method set some data and write entire Quiddity record with all indexes!
func (pa *PersonAuthentication) SaveNew() (err protocol.Error) {
	err = pa.Set()
	if err != nil {
		return
	}
	pa.IndexRecordIDForPersonID()
	pa.IndexPersonIDForRegisterTime()
	if pa.ReferentPersonID != [32]byte{} {
		pa.IndexPersonIDForReferentPersonID()
	}
	return
}

// Set method set some data and write entire PersonAuthentication record!
func (pa *PersonAuthentication) Set() (err protocol.Error) {
	pa.RecordStructureID = personAuthenticationStructureID
	pa.RecordSize = pa.LenAsSyllab()
	pa.WriteTime = time.Now()
	pa.OwnerAppID = protocol.OS.AppManifest().AppUUID()

	var req = ganjine.SetRecordReq{
		Type:   ganjine.RequestTypeBroadcast,
		Record: pa.ToSyllab(),
	}
	pa.RecordID = sha3.Sum256(req.Record[32:])
	copy(req.Record[0:], pa.RecordID[:])

	err = gsdk.SetRecord(&req)
	if err != nil {
		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Ganjine - Set Record:", err)
		}
		// TODO::: Handle error situation
	}

	return
}

// GetByRecordID method read all existing record data by given RecordID!
func (pa *PersonAuthentication) GetByRecordID() (err protocol.Error) {
	var req = ganjine.GetRecordReq{
		RecordID:          pa.RecordID,
		RecordStructureID: personAuthenticationStructureID,
	}
	var res *ganjine.GetRecordRes
	res, err = gsdk.GetRecord(&req)
	if err != nil {
		return
	}

	err = pa.FromSyllab(res.Record)
	if err != nil {
		return
	}

	if pa.RecordStructureID != personAuthenticationStructureID {
		err = ganjine.ErrMisMatchedStructureID
	}
	return
}

// GetLastByPersonID method find and read last version of record by given PersonID!
func (pa *PersonAuthentication) GetLastByPersonID() (err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pa.hashPersonIDForRecordID(),
		Offset:   18446744073709551615,
		Limit:    1,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	if err != nil {
		return
	}

	pa.RecordID = indexRes.IndexValues[0]
	err = pa.GetByRecordID()
	if err.Equal(ganjine.ErrMisMatchedStructureID) {
		protocol.App.Log(log.WarnEvent(domainEnglish, "Platform collapsed!! HASH Collision Occurred on", personAuthenticationStructureID)
	}
	return
}

/*
	-- PRIMARY INDEXES --
*/

// IndexRecordIDForPersonID save RecordID chain for PersonID
func (pa *PersonAuthentication) IndexRecordIDForPersonID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashPersonIDForRecordID(),
		IndexValue: pa.RecordID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Ganjine - Set Index:", err)
		}
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *PersonAuthentication) hashPersonIDForRecordID() (hash [32]byte) {
	var buf = make([]byte, 40) // 8+32
	syllab.SetUInt64(buf, 0, personAuthenticationStructureID)
	copy(buf[8:], pa.PersonID[:])
	return sha3.Sum256(buf)
}

/*
	-- SECONDARY INDEXES --
*/

// IndexPersonIDForRegisterTime index pa.WriteTime to retrieve all register person on specific time in hour rate.
// Each year is 8760 hour (365*24) that indicate we have 8760 index record each year!
func (pa *PersonAuthentication) IndexPersonIDForRegisterTime() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashWriteTimeforPersonIDHourly(),
		IndexValue: pa.PersonID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Ganjine - Set Index:", err)
		}
		// TODO::: we must retry more due to record wrote successfully before this func!
	}
}

func (pa *PersonAuthentication) hashWriteTimeforPersonIDHourly() (hash [32]byte) {
	const field = "WriteTime"
	var buf = make([]byte, 16) // 8+8
	syllab.SetUInt64(buf, 0, personAuthenticationStructureID)
	syllab.SetInt64(buf, 8, pa.WriteTime.RoundToHour())
	copy(buf[16:], field)
	return sha3.Sum256(buf)
}

// IndexPersonIDForReferentPersonID index pa.ReferentPersonID to retrieve record fast later.
func (pa *PersonAuthentication) IndexPersonIDForReferentPersonID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pa.hashIfReferentPersonIDForPersonID(),
		IndexValue: pa.PersonID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Ganjine - Set Index:", err)
		}
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pa *PersonAuthentication) hashIfReferentPersonIDForPersonID() (hash [32]byte) {
	const field = "IfReferentPersonID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, personAuthenticationStructureID)
	copy(buf[8:], pa.ReferentPersonID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

/*
	-- Syllab Encoder & Decoder --
*/

func (pa *PersonAuthentication) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(payload)) < pa.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(pa.AppInstanceID[:], payload[88:])
	copy(pa.UserConnectionID[:], payload[120:])
	copy(pa.PersonID[:], payload[152:])
	copy(pa.ReferentPersonID[:], payload[184:])
	pa.Status = PersonAuthenticationStatus(syllab.GetUInt8(payload, 216))

	copy(pa.PasswordHash[:], payload[217:])
	copy(pa.OTPPattern[:], payload[249:])
	pa.OTPAdditional = syllab.GetInt32(payload, 281)
	copy(pa.PublicKey[:], payload[285:])
	return
}

func (pa *PersonAuthentication) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(payload[88:], pa.AppInstanceID[:])
	copy(payload[120:], pa.UserConnectionID[:])
	copy(payload[152:], pa.PersonID[:])
	copy(payload[184:], pa.ReferentPersonID[:])
	syllab.SetUInt8(payload, 216, uint8(pa.Status))

	copy(payload[217:], pa.PasswordHash[:])
	copy(payload[249:], pa.OTPPattern[:])
	syllab.SetInt32(payload, 281, pa.OTPAdditional)
	copy(payload[285:], pa.PublicKey[:])
	return heapIndex
}

func (pa *PersonAuthentication) LenAsSyllab() uint64 {
	return uint64(pa.LenOfSyllabStack() + pa.LenOfSyllabHeap())
}
func (pa *PersonAuthentication) LenOfSyllabStack() uint32     { return 317 }
func (pa *PersonAuthentication) LenOfSyllabHeap() (ln uint32) { return }

/*
	-- Record types --
*/

// PersonAuthenticationStatus indicate PersonAuthentication record status
type PersonAuthenticationStatus uint8

// PersonAuthentication status
const (
	PersonAuthenticationUnset              PersonAuthenticationStatus = iota
	PersonAuthenticationInactive                                      // person had been inactive and can't be use now!
	PersonAuthenticationBlocked                                       // person had been blocked and can't be use now!
	PersonAuthenticationNotForceUse2Factor                            // authenticate person just with Password
	PersonAuthenticationForceUse2Factor                               // authenticate person with Password + OTP
	PersonAuthenticationMustChangePassword                            // user must change password to increase security!
)
