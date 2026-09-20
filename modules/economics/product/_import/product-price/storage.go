/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"golang.org/x/crypto/sha3"

	"libgo/ganjine"
	"libgo/math"
	"libgo/pehrest"
	"libgo/price"
	"libgo/syllab"
)

const (
	quiddityPriceStructureID uint64 = 2759922966933000947
)

var quiddityPriceStructure = ds.DataStructure{
	URN:             "urn:giti:sabz.city:data-structure:product-price",
	ID:              2759922966933000947,
	IssueDate:       1607422485,
	ExpiryDate:      0,
	ExpireInFavorOf: "",
	Status:          protocol.Software_PreAlpha,
	Structure:       QuiddityPrice{},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "Product Price",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "",
	},
	TAGS: []string{
		"",
	},
}

// QuiddityPrice ---Read locale description in QuiddityPriceStructure---
type QuiddityPrice struct {
	RequestID  [16]byte // user-request domain
	QuiddityID [16]byte `index-hash:"ObjectID[pair,Currency]"`
	OrgID      [16]byte `index-hash:"QuiddityID"` // Sell can be register just by producer organization
	Currency   price.Currency
	BasicPrice price.Amount
	Tax        math.PerMyriad // VAT as Value-Added-Tax is bad name for a robbery!
	Price      price.Amount   // Just use if seller don't discount in the base price.
}

// SaveNew method set some data and write entire QuiddityPrice record with all indexes!
func (pp *QuiddityPrice) SaveNew() (err protocol.Error) {
	err = pp.Set()
	if err != nil {
		return
	}

	pp.IndexObjectIDForQuiddityID()
	pp.IndexQuiddityIDForOrgID()
	return
}

// Update method set some data and write entire QuiddityPrice record with needed indexes!
func (pp *QuiddityPrice) Update() (err protocol.Error) {
	err = pp.Set()
	if err != nil {
		return
	}

	pp.IndexObjectIDForQuiddityID()
	return
}

// Set method set some data and write entire QuiddityPrice record!
func (pp *QuiddityPrice) Set() (err protocol.Error) {
	var req = ganjine.SetRecordReq{
		Type:   ganjine.RequestTypeBroadcast,
		Record: pp.ToSyllab(),
	}
	pp.ObjectID = sha3.Sum256(req.Record[32:])
	copy(req.Record[0:], pp.ObjectID[:])

	err = gsdk.SetRecord(&req)
	if err != nil {
		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Ganjine - Set Record Error:", err)
		}
		// TODO::: Handle error situation
	}

	return
}

// GetByObjectID read existing record data by given ObjectID!
func (pp *QuiddityPrice) GetByObjectID() (err protocol.Error) {
	var req = ganjine.GetRecordReq{
		ObjectID:          pp.ObjectID,
		RecordStructureID: quiddityPriceStructureID,
	}
	var res *ganjine.GetRecordRes
	res, err = gsdk.GetRecord(&req)
	if err != nil {
		return
	}

	err = pp.FromSyllab(res.Record)
	if err != nil {
		return
	}

	if pp.RecordStructureID != quiddityPriceStructureID {
		protocol.App.Log(log.WarnEvent(domainEnglish, "Platform collapsed!! HASH Collision Occurred on", quiddityPriceStructureID)
		err = ganjine.ErrMisMatchedStructureID
	}
	return
}

// GetLastByQuiddityID method read last existing record data by given QuiddityID!
func (pp *QuiddityPrice) GetLastByQuiddityID() (err protocol.Error) {
	var indexReq = &pehrest.HashGetValuesReq{
		IndexKey: pp.hashQuiddityIDForObjectID(),
		Offset:   18446744073709551615,
		Limit:    1,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexReq)
	if err != nil {
		return
	}

	pp.ObjectID = indexRes.IndexValues[0]
	err = pp.GetByObjectID()
	if err.Equal(ganjine.ErrMisMatchedStructureID) {
		protocol.App.Log(log.WarnEvent(domainEnglish, "Platform collapsed!! HASH Collision Occurred on", productAuctionStructureID)
	}
	return
}

/*
	-- Search Methods --
*/

// FindRecordsIDsByQuiddityID find RecordsIDs by given ID
func (pp *QuiddityPrice) FindRecordsIDsByQuiddityID(offset, limit uint64) (RecordsIDs [][32]byte, err protocol.Error) {
	var indexRequest = &pehrest.HashGetValuesReq{
		IndexKey: pp.hashQuiddityIDForObjectID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexRequest)
	RecordsIDs = indexRes.IndexValues
	return
}

// FindQuiddityIDsByOrgID find QuiddityIDs by given OrgID
func (pp *QuiddityPrice) FindQuiddityIDsByOrgID(offset, limit uint64) (IDs [][32]byte, err protocol.Error) {
	var indexRequest = &pehrest.HashGetValuesReq{
		IndexKey: pp.hashOrgIDForQuiddityID(),
		Offset:   offset,
		Limit:    limit,
	}
	var indexRes *pehrest.HashGetValuesRes
	indexRes, err = psdk.HashGetValues(indexRequest)
	IDs = indexRes.IndexValues
	return
}

/*
	-- PRIMARY INDEXES --
*/

// IndexObjectIDForQuiddityID save ObjectID chain for QuiddityID
// Call in each update to the exiting record!
func (pp *QuiddityPrice) IndexObjectIDForQuiddityID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pp.hashQuiddityIDForObjectID(),
		IndexValue: pp.ObjectID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Ganjine - Set Index Error:", err)
		}
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pp *QuiddityPrice) hashQuiddityIDForObjectID() (hash [32]byte) {
	const field = "QuiddityID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, quiddityPriceStructureID)
	copy(buf[8:], pp.QuiddityID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

/*
	-- SECONDARY INDEXES --
*/

// IndexQuiddityIDForOrgID save QuiddityID chain for OrgID.
// Don't call in update to an exiting record!
func (pp *QuiddityPrice) IndexQuiddityIDForOrgID() {
	var indexRequest = pehrest.HashSetValueReq{
		Type:       ganjine.RequestTypeBroadcast,
		IndexKey:   pp.hashOrgIDForQuiddityID(),
		IndexValue: pp.QuiddityID,
	}
	var err = psdk.HashSetValue(&indexRequest)
	if err != nil {
		if protocol.LogMode_Debug {
			protocol.App.Log(log.DebugEvent(domainEnglish, "Ganjine - Set Index Error:", err)
		}
		// TODO::: we must retry more due to record wrote successfully!
	}
}

func (pp *QuiddityPrice) hashOrgIDForQuiddityID() (hash [32]byte) {
	const field = "OrgID"
	var buf = make([]byte, 40+len(field)) // 8+32
	syllab.SetUInt64(buf, 0, quiddityPriceStructureID)
	copy(buf[8:], pp.OrgID[:])
	copy(buf[40:], field)
	return sha3.Sum256(buf)
}

/*
	-- LIST FIELDS --
*/

// ??

/*
	-- Temporary INDEXES & LIST --
*/

// ??

/*
	-- Syllab Encoder & Decoder --
*/

func (pp *QuiddityPrice) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < pp.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(pp.AppInstanceID[:], buf[88:])
	copy(pp.UserConnectionID[:], buf[120:])
	copy(pp.OrgID[:], buf[152:])
	copy(pp.QuiddityID[:], buf[184:])

	pp.MaterialsPercent = math.PerMyriad(syllab.GetUInt16(buf, 216))
	pp.MaterialsCost = price.Amount(syllab.GetInt64(buf, 218))
	pp.LaborPercent = math.PerMyriad(syllab.GetUInt16(buf, 226))
	pp.LaborCost = price.Amount(syllab.GetInt64(buf, 228))
	pp.InvestmentsPercent = math.PerMyriad(syllab.GetUInt16(buf, 236))
	pp.InvestmentsCost = price.Amount(syllab.GetInt64(buf, 238))
	pp.TotalCost = price.Amount(syllab.GetInt64(buf, 246))

	pp.Markup = math.PerMyriad(syllab.GetUInt16(buf, 254))
	pp.WholesaleProfit = price.Amount(syllab.GetInt64(buf, 256))
	pp.Margin = math.PerMyriad(syllab.GetUInt16(buf, 264))
	pp.RetailProfit = price.Amount(syllab.GetInt64(buf, 266))

	pp.TaxPercent = math.PerMyriad(syllab.GetUInt16(buf, 274))
	pp.Tax = price.Amount(syllab.GetInt64(buf, 276))

	pp.Price = price.Amount(syllab.GetInt64(buf, 284))
	return
}

func (pp *QuiddityPrice) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	copy(buf[88:], pp.AppInstanceID[:])
	copy(buf[120:], pp.UserConnectionID[:])
	copy(buf[152:], pp.OrgID[:])
	copy(buf[184:], pp.QuiddityID[:])

	syllab.SetUInt16(buf, 216, uint16(pp.MaterialsPercent))
	syllab.SetInt64(buf, 218, int64(pp.MaterialsCost))
	syllab.SetUInt16(buf, 226, uint16(pp.LaborPercent))
	syllab.SetInt64(buf, 228, int64(pp.LaborCost))
	syllab.SetUInt16(buf, 236, uint16(pp.InvestmentsPercent))
	syllab.SetInt64(buf, 238, int64(pp.InvestmentsCost))
	syllab.SetInt64(buf, 246, int64(pp.TotalCost))

	syllab.SetUInt16(buf, 254, uint16(pp.Markup))
	syllab.SetInt64(buf, 256, int64(pp.WholesaleProfit))
	syllab.SetUInt16(buf, 264, uint16(pp.Margin))
	syllab.SetInt64(buf, 266, int64(pp.RetailProfit))

	syllab.SetUInt16(buf, 274, uint16(pp.TaxPercent))
	syllab.SetInt64(buf, 276, int64(pp.Tax))

	syllab.SetInt64(buf, 284, int64(pp.Price))
	return
}

func (pp *QuiddityPrice) LenOfSyllabStack() uint32 {
	return 292
}

func (pp *QuiddityPrice) LenOfSyllabHeap() (ln uint32) {
	return
}

func (pp *QuiddityPrice) LenAsSyllab() uint64 {
	return uint64(pp.LenOfSyllabStack() + pp.LenOfSyllabHeap())
}
