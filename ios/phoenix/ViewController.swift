//
//  ViewController.swift
//  phoenix
//
//  Created by Bill Liu on 3/28/20.
//  Copyright © 2020 Bill Liu. All rights reserved.
//

import Foundation
import UIKit
import MapKit

protocol HandleMapSearch {
    func dropPinZoomIn(placemark: MKPlacemark)
}

class ViewController: UIViewController {
    let locationManager = CLLocationManager()
    @IBOutlet weak var mapView: MKMapView!
    
    var resultSearchController: UISearchController? = nil
    var selectedPin: MKPlacemark? = nil
    var locationFormTableViewController: LocationFormTable? = nil
    
    var uniqueSessionId: String = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.requestWhenInUseAuthorization()
        locationManager.requestLocation()
        
        let locationSearchTable = storyboard!.instantiateViewController(withIdentifier: "LocationSearchTable") as! LocationSearchTable
        resultSearchController = UISearchController(searchResultsController: locationSearchTable)
        resultSearchController?.searchResultsUpdater = locationSearchTable
        resultSearchController?.hidesNavigationBarDuringPresentation = false
        definesPresentationContext = true
        
        locationFormTableViewController = storyboard!.instantiateViewController(identifier: "LocationFormTable")
        
        let searchBar = resultSearchController!.searchBar
        searchBar.sizeToFit()
        searchBar.placeholder = "Search for visited location"
        navigationItem.titleView = resultSearchController?.searchBar
        locationSearchTable.mapView = mapView
        locationSearchTable.handleMapSearchDelegate = self
        
        uniqueSessionId = NSUUID().uuidString
        self.overrideUserInterfaceStyle = .dark
    }
    
    func setRegion(_ center: CLLocationCoordinate2D) {
        let span = MKCoordinateSpan.init(latitudeDelta: 0.05, longitudeDelta: 0.05)
        let region = MKCoordinateRegion.init(center: center, span: span)
        mapView.setRegion(region, animated: true)
    }
    
    @objc func uploadData() {
        if let selectedPin = selectedPin {
//            let mapItem = MKMapItem(placemark: selectedPin)
            if let locationFormTableViewController = locationFormTableViewController {
                locationFormTableViewController.id = uniqueSessionId
                locationFormTableViewController.latitude = String(selectedPin.coordinate.latitude)
                locationFormTableViewController.longitude = String(selectedPin.coordinate.longitude)
//                locationFormTableViewController.timestamp = String(Date().currentTimeMillis())
//                performSegue(withIdentifier: "toData", sender: nil)
                locationFormTableViewController.location = selectedPin.title
                self.navigationController!.pushViewController(locationFormTableViewController, animated: true)
            }
        }
    }
}

extension ViewController: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if status == .authorizedWhenInUse {
            locationManager.requestLocation()
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        if let location = locations.first {
            self.setRegion(location.coordinate)
            print("location: \(location)")
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("error: \(error)")
    }
}

extension ViewController: HandleMapSearch {
    func dropPinZoomIn(placemark: MKPlacemark) {
        // cache the pin
        selectedPin = placemark
        
        // clear existing pins
        mapView.removeAnnotations(mapView.annotations)
        let annotation = MKPointAnnotation()
        annotation.coordinate = placemark.coordinate
        print("coordinates: \(placemark.coordinate)")
        annotation.title = placemark.name
        
        if
            let city = placemark.locality,
            let state = placemark.administrativeArea {
                annotation.subtitle = "\(city) \(state)"
            }
        
        mapView.addAnnotation(annotation)
        self.setRegion(placemark.coordinate)
    }
}

extension ViewController: MKMapViewDelegate {
    func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
        if annotation is MKUserLocation { return nil }
        
        let reuseId = "pin"
        var pinView = mapView.dequeueReusableAnnotationView(withIdentifier: reuseId) as? MKPinAnnotationView
        pinView = MKPinAnnotationView(annotation: annotation, reuseIdentifier: reuseId)
        pinView?.pinTintColor = UIColor.blue
        pinView?.canShowCallout = true
        let smallSquare = CGSize(width: 30, height: 30)
        let button = UIButton(frame: CGRect(origin: CGPoint.zero, size: smallSquare))
        button.setBackgroundImage(UIImage(named: "arrow"), for: UIControl.State.normal)
        button.addTarget(self, action: #selector(self.uploadData), for: .touchUpInside)
        pinView?.leftCalloutAccessoryView = button
        return pinView
    }
}

extension Date {
    func currentTimeMillis() -> Int64 {
        return Int64(self.timeIntervalSince1970 * 1000)
    }
}

extension UINavigationController {
    func pushViewController(_ viewController: UIViewController, animated: Bool, completion: @escaping () -> Void) {
        pushViewController(viewController, animated: animated)

        if animated, let coordinator = transitionCoordinator {
            coordinator.animate(alongsideTransition: nil) { _ in
                completion()
            }
        } else {
            completion()
        }
    }

    func popViewController(animated: Bool, completion: @escaping () -> Void) {
        popViewController(animated: animated)

        if animated, let coordinator = transitionCoordinator {
            coordinator.animate(alongsideTransition: nil) { _ in
                completion()
            }
        } else {
            completion()
        }
    }
}
