//
//  LocationFormTable.swift
//  phoenix
//
//  Created by Bill Liu on 3/28/20.
//  Copyright © 2020 Bill Liu. All rights reserved.
//

import UIKit

class LocationFormTable: UITableViewController {
    @IBOutlet weak var idTextField: UITextField!
    @IBOutlet weak var longitudeTextField: UITextField!
    @IBOutlet weak var latitudeTextField: UITextField!
    @IBOutlet weak var timestampTextField: UITextField!
    @IBOutlet weak var notesTextField: UITextField!
    @IBOutlet weak var sendDataButton: UIBarButtonItem!
    
    var id: String?
    var location: String?
    var longitude: String?
    var latitude: String?
    var timestamp: Int64?
    var notes: String?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        if
            let id = id,
            let longitude = longitude,
            let latitude = latitude
        {
            idTextField.text = id
            longitudeTextField.text = longitude
            latitudeTextField.text = latitude
            
            let formatter = DateFormatter()
            formatter.dateFormat = "yyyy-MM-dd"
            let myString = formatter.string(from: Date())
            timestampTextField.text = myString
        }
        
        idTextField.isUserInteractionEnabled = false
        longitudeTextField.isUserInteractionEnabled = false
        latitudeTextField.isUserInteractionEnabled = false
        
        let datePicker = UIDatePicker.init()
        datePicker.setDate(Date().self, animated: true)
        datePicker.addTarget(self, action: #selector(updateDate(_:)), for: UIControl.Event.valueChanged)
        self.timestampTextField.inputView = datePicker

        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        // self.navigationItem.rightBarButtonItem = self.editButtonItem
    }
    
    @objc func updateDate(_ sender: Any) {
        let picker = self.timestampTextField!.inputView as! UIDatePicker
        timestamp = picker.date.currentTimeMillis()
        
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        let myString = formatter.string(from: picker.date)
        self.timestampTextField.text = myString
    }
    
    @IBAction func sendData(_ sender: Any) {
        let rootVC = self.navigationController!.viewControllers.first as! PatientHistoryTable
        var newRecord = historyRecord.init()
        newRecord.location = location!
        newRecord.time = self.timestampTextField.text!
        newRecord.unixTime = timestamp!
        
        rootVC.records.append(newRecord)
        self.navigationController!.popToRootViewController(animated: true)
    }
    
    // MARK: - Table view data source

    /*override func numberOfSections(in tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 0
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return 0
    }*/

    /*
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "reuseIdentifier", for: indexPath)

        // Configure the cell...

        return cell
    }
    */

    /*
    // Override to support conditional editing of the table view.
    override func tableView(_ tableView: UITableView, canEditRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the specified item to be editable.
        return true
    }
    */

    /*
    // Override to support editing the table view.
    override func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCell.EditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == .delete {
            // Delete the row from the data source
            tableView.deleteRows(at: [indexPath], with: .fade)
        } else if editingStyle == .insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
    */

    /*
    // Override to support rearranging the table view.
    override func tableView(_ tableView: UITableView, moveRowAt fromIndexPath: IndexPath, to: IndexPath) {

    }
    */

    /*
    // Override to support conditional rearranging of the table view.
    override func tableView(_ tableView: UITableView, canMoveRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
    */

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
