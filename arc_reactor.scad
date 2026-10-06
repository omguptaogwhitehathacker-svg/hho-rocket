// Decorative, non-functional triangular arc-reactor prop.
// Export the rendered model as STL before importing into Tinkercad.
// The ports, wires, and +/- marks are cosmetic only. Do not connect to gas,
// water pressure, mains electricity, batteries, or any live system.

$fn = 48;

outer = [[0, 46], [-52, -34], [52, -34]];
inner = [[0, 42], [-47, -31], [47, -31]];

module triangular_prism(points, height) {
    linear_extrude(height = height) polygon(points);
}

module reactor_body() {
    // Thin base and perimeter walls surround, but do not contain, the rods.
    difference() {
        triangular_prism(outer, 6);
        translate([0, 0, 1]) triangular_prism(inner, 5);
    }
    difference() {
        translate([0, 0, 6]) triangular_prism(outer, 28);
        translate([0, 0, 6]) triangular_prism(inner, 28);
    }
}

module top_part() {
    // Matching upper rim keeps the triangular container visually complete.
    difference() {
        translate([0, 0, 32]) triangular_prism(outer, 2);
        translate([0, 0, 32]) triangular_prism(inner, 2);
    }
}

module rod(x, y, index) {
    translate([x, y, 7]) {
        cylinder(h = 22, r = 2.15);
        translate([0, 0, 22]) cylinder(h = 1.5, r = 2.75);
        translate([0, 0, 23.5])
            linear_extrude(height = 0.7)
                text(index % 2 == 0 ? "+" : "-", size = 3.2,
                     halign = "center", valign = "center");
    }
}

module port(x) {
    // Cosmetic bottom-facing valve body and cap; no open channel is modeled.
    translate([x, -32, 0]) {
        cylinder(h = 6, r = 4.5);
        translate([0, 0, -4]) cylinder(h = 4, r = 6);
        translate([0, 0, -6]) cylinder(h = 2, r = 3.5);
    }
}

module beam(point_a, point_b, z, radius = 0.6) {
    hull() {
        translate([point_a[0], point_a[1], z]) sphere(r = radius);
        translate([point_b[0], point_b[1], z]) sphere(r = radius);
    }
}

module wire_loop(z) {
    // One short triangular wire loop follows all three rod rows.
    loop_points = [[0, 39], [-44, -28], [44, -28]];
    beam(loop_points[0], loop_points[1], z);
    beam(loop_points[1], loop_points[2], z);
    beam(loop_points[2], loop_points[0], z);
}

module label(text_value, x, y, size = 4) {
    translate([x, y, 6.1])
        linear_extrude(height = 0.7)
            text(text_value, size = size, halign = "center", valign = "center");
}

reactor_body();
top_part();

// Exactly 12 separate carbon-look rods, equally spaced along the three sides.
rod(-6, 29, 0);
rod(-15, 16, 1);
rod(-24, 3, 2);
rod(-33, -10, 3);
rod(6, 29, 4);
rod(15, 16, 5);
rod(24, 3, 6);
rod(33, -10, 7);
rod(-24, -27, 8);
rod(-8, -27, 9);
rod(8, -27, 10);
rod(24, -27, 11);

// Cosmetic gas, water inlet, and water outlet positions along the bottom.
port(-25); // GAS
port(0);   // WATER IN
port(25);  // WATER OUT
label("GAS", -25, -20, 4);
label("WATER IN", 0, -20, 3.5);
label("WATER OUT", 25, -20, 3.2);
label("CARBON RODS", 0, 0, 4.5);
label("WIRES", 0, 13, 3.5);

// Exactly two thin wire loops, kept inside the triangular outline.
wire_loop(14);
wire_loop(24);
