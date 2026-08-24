// Non-functional, static rocket display model.
// Body diameter is 50.8 mm (2 inches). All details are molded into one body.
// The long body, small fins, and bell nozzle use NASA launch-vehicle styling.
// The nozzle and ignition-wire details are cosmetic only.

$fn = 64;

rocket_diameter = 50.8;
rocket_radius = rocket_diameter / 2;
shell_thickness = 2.5;
body_height = 180;
core_radius = 12;
core_height = 154;

module inspection_window(angle) {
    rotate([0, 0, angle])
        translate([rocket_radius - 1, -7, 31])
            cube([shell_thickness + 4, 14, 42]);
}

module body_shell() {
    difference() {
        cylinder(h = body_height, r = rocket_radius);
        translate([0, 0, shell_thickness])
            cylinder(h = body_height, r = rocket_radius - shell_thickness);
        inspection_window(0);
        inspection_window(180);
    }
}

module internal_core() {
    translate([0, 0, 8]) {
        cylinder(h = core_height, r = core_radius);
        translate([0, 0, core_height]) cylinder(h = 4, r = 15);
        translate([0, 0, -4]) cylinder(h = 4, r = 15);
    }
}

module core_detail(z) {
    translate([0, 0, z])
        difference() {
            cylinder(h = 3, r = core_radius + 1.5);
            translate([0, 0, -0.1]) cylinder(h = 3.2, r = core_radius - 1.5);
        }
}

module core_support(z, angle) {
    rotate([0, 0, angle])
        translate([core_radius - 1, -2, z])
            cube([rocket_radius - shell_thickness - core_radius, 4, 3]);
}

module nose() {
    translate([0, 0, body_height - 1])
        cylinder(h = 6, r = rocket_radius);
    translate([0, 0, body_height + 5])
        cylinder(h = 42, r1 = rocket_radius, r2 = 3);
}

module molded_fin(angle) {
    rotate([0, 0, angle])
        translate([rocket_radius - 3, -1.5, 0])
            rotate([90, 0, 0])
                linear_extrude(height = 4)
                    polygon([[0, 8], [11, 12], [10, 38], [0, 46]]);
}

module wire_detail(angle) {
    rotate([0, 0, angle])
        translate([rocket_radius - 1.2, 0, 112])
            rotate([0, 18, 0])
                cylinder(h = 25, r = 1.2);
}

module body_bands() {
    for (z = [22, 158])
        translate([0, 0, z])
            difference() {
                cylinder(h = 2.5, r = rocket_radius + 0.8);
                translate([0, 0, -0.1])
                    cylinder(h = 2.7, r = rocket_radius - 0.8);
            }
}

module decorative_nozzle() {
    // Solid revolved display profile: no exhaust channel or live-system feature.
    // The top collar overlaps the body, then curves inward to a short throat
    // before curving outward to a 25.4 mm (1 inch) cosmetic exit.
    nozzle_profile = [
        [0, 1], [24, 1], [24, 0], [22, -1],
        [19, -3], [16, -6], [12, -9], [8, -12],
        [5.5, -15], [5.5, -19], [6, -21], [7, -23],
        [9, -25], [11, -27], [12.2, -29], [12.7, -31],
        [12.7, -33], [0, -33]
    ];
    rotate_extrude(convexity = 10)
        polygon(nozzle_profile);
}

// One connected body with a visible fixed interior.
union() {
    body_shell();
    internal_core();
    core_detail(25);
    core_detail(49);
    core_detail(73);
    core_detail(101);
    core_detail(133);
    core_support(42, 0);
    core_support(42, 90);
    core_support(124, 180);
    core_support(124, 270);
    body_bands();

    // Integrated aerodynamic styling and fixed nose.
    nose();
    molded_fin(0);
    molded_fin(90);
    molded_fin(180);
    molded_fin(270);

    // Two molded cosmetic ignition-wire representations.
    wire_detail(0);
    wire_detail(180);

    decorative_nozzle();
}